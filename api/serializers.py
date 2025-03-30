from rest_framework import serializers
from api.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Transaction
        fields="__all__"
        read_only_fields=["id","created_date"]


class TransactionSummarySerializer(serializers.Serializer):
    total_expense=serializers.DecimalField(max_digits=10,decimal_places=2)
    total_income=serializers.DecimalField(max_digits=10,decimal_places=2)
    category_summary=serializers.DictField(child=serializers.DecimalField(max_digits=10,decimal_places=2))

        