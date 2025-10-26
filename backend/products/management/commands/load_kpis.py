from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum
from products.models import Product, Sale, Review, Return, SuggestedAction
import json
import os


class Command(BaseCommand):
    """
    Custom Django command that clears existing product data and reloads
    fresh information directly from the provided JSON dataset.
    This version intentionally avoids any CSV merging or secondary data imports.
    """

    help = "Reloads product, sales, review, and return data purely from the JSON dataset."

    def handle(self, *args, **kwargs):
        base_path = "products/data"
        dataset_path = os.path.join(base_path, "sde2_merchtech_dataset.txt")

        # -------------------------------------------------------------
        # STEP 1: Clean all old records before reloading
        # -------------------------------------------------------------
        self.stdout.write("🧹 Removing old records...")
        with transaction.atomic():
            Sale.objects.all().delete()
            Review.objects.all().delete()
            Return.objects.all().delete()
            SuggestedAction.objects.all().delete()
            Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Old data successfully cleared."))

        # -------------------------------------------------------------
        # STEP 2: Load dataset from JSON
        # -------------------------------------------------------------
        if not os.path.exists(dataset_path):
            self.stdout.write(self.style.ERROR(f"❌ Dataset not found at: {dataset_path}"))
            return

        with open(dataset_path, "r") as file:
            dataset = json.load(file)

        product_entries = dataset.get("products", [])
        self.stdout.write(f"📦 Found {len(product_entries)} product records to import.")

        for item in product_entries:
            asin = str(item.get("asin", "")).strip()
            if not asin:
                self.stdout.write(self.style.WARNING("⚠️ Skipped record with missing ASIN."))
                continue

            # Create product entry
            product = Product.objects.create(
                asin=asin,
                name=item.get("product", "Unnamed Product")
            )

            # ---------------- Sales Data ----------------
            for sale in item.get("sales", []):
                Sale.objects.update_or_create(
                    product=product,
                    week=sale["week"],
                    defaults={
                        "units_sold": sale["units_sold"],
                        "gmv": sale["gmv"],
                        "refunds": sale["refunds"],
                    },
                )

            # ---------------- Review Data ----------------
            for review in item.get("reviews", []):
                Review.objects.create(
                    product=product,
                    review_text=review.get("review_text", "").strip(),
                    rating=review.get("rating", 0),
                )

            # ---------------- Return Data ----------------
            # Combine duplicate return reasons and sum their counts
            merged_reasons = {}
            for ret in item.get("returns", []):
                reason = ret.get("return_reason", "").strip()
                count = int(ret.get("count", 0))
                if reason:
                    merged_reasons[reason] = merged_reasons.get(reason, 0) + count

            for reason, total_count in merged_reasons.items():
                Return.objects.create(
                    product=product,
                    return_reason=reason,
                    count=total_count,
                )

        self.stdout.write(self.style.SUCCESS("✅ Dataset successfully loaded from JSON."))

        # -------------------------------------------------------------
        # STEP 3: Recalculate product-level metrics
        # -------------------------------------------------------------
        for product in Product.objects.all():
            sales_qs = Sale.objects.filter(product=product)
            reviews_qs = Review.objects.filter(product=product)
            returns_qs = Return.objects.filter(product=product)

            product.total_gmv = sales_qs.aggregate(total=Sum("gmv"))["total"] or 0
            product.total_units = sales_qs.aggregate(total=Sum("units_sold"))["total"] or 0
            product.total_refunds = sales_qs.aggregate(total=Sum("refunds"))["total"] or 0
            product.average_rating = (
                round(sum(r.rating for r in reviews_qs) / len(reviews_qs), 2)
                if reviews_qs else 0
            )
            product.save()

        self.stdout.write(self.style.SUCCESS("✅ Product aggregates updated."))

        # -------------------------------------------------------------
        # STEP 4: Generate automatic improvement suggestions
        # -------------------------------------------------------------
        for product in Product.objects.all():
            suggestion_text = self._generate_recommendations(product)
            self.stdout.write(f"🧠 {product.name}: {suggestion_text}")

        self.stdout.write(self.style.SUCCESS("✅ Insights generated successfully."))

    # -----------------------------------------------------------------
    # INTERNAL METHOD: Suggestion Generation
    # -----------------------------------------------------------------
    def _generate_recommendations(self, product):
        """Create meaningful suggestions for a product based on its feedback, returns, and ratings."""
        reviews = Review.objects.filter(product=product)
        returns = Return.objects.filter(product=product)
        avg_rating = product.average_rating or 0
        combined_reviews = " ".join([r.review_text.lower() for r in reviews])
        return_reasons = list(returns.values_list("return_reason", flat=True))

        recommendations = set()

        # Common issues mapped to corrective actions
        issue_map = {
            "late delivery": "Optimize supply chain and partner logistics to improve on-time delivery.",
            "defective product": "Perform tighter quality control during manufacturing and pre-shipment inspections.",
            "damaged item": "Enhance packaging standards and review warehouse handling procedures.",
            "wrong color": "Audit image-to-product color accuracy and improve product detail page descriptions.",
            "size mismatch": "Update sizing guides and improve dimensional accuracy in listings.",
            "delayed shipment": "Work closely with carriers to improve dispatch and reduce delay rates.",
            "poor quality": "Reassess supplier quality standards and perform regular QA audits."
       }

        # Link known issues to corresponding actions
        for reason in return_reasons:
            for keyword, action in issue_map.items():
                if keyword in reason.lower():
                    recommendations.add(action)

        # Sentiment-based logic (keywords from reviews)
        if "defect" in combined_reviews or "broken" in combined_reviews:
            recommendations.add("Strengthen pre-shipment inspection and product testing.")
        if "damage" in combined_reviews:
            recommendations.add("Introduce protective packaging for vulnerable components.")
        if "late" in combined_reviews or "delay" in combined_reviews:
            recommendations.add("Work with faster, more reliable couriers to reduce delays.")
        if "wrong" in combined_reviews or "mismatch" in combined_reviews:
            recommendations.add("Validate product details before dispatch to avoid mismatched shipments.")
        if "size" in combined_reviews:
            recommendations.add("Provide clearer sizing information to minimize fit-related returns.")

        # Additional suggestions based on overall rating trends
        if avg_rating < 2.5:
            recommendations.add("Immediate review required — identify top customer pain points.")
        elif 2.5 <= avg_rating < 3.5:
            recommendations.add("Moderate satisfaction — address frequent feedback topics to boost ratings.")
        elif avg_rating >= 4.5:
            recommendations.add("High performer — continue promotion and maintain consistency.")

        # Select top few actionable insights
        if recommendations:
            suggestion_text = " ".join(list(recommendations)[:3])
        else:
            suggestion_text = "Product is performing well — continue monitoring feedback and logistics KPIs."

        # Store or update suggestion record
        SuggestedAction.objects.update_or_create(
            product=product,
            defaults={
                "action_text": suggestion_text,
                "is_manual": False,
                "generated_on": timezone.now(),
            },
        )

        return suggestion_text
    