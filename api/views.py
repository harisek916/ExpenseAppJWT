from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions

from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import TransactionSerializer,TransactionSummarySerializer
from api.models import Transaction


# Create your views here.


class TransactionView(viewsets.ModelViewSet):
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]


class TransactionSummaryView(APIView):

    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        cur_month=timezone.now().month
        cur_year=timezone.now().year
        transaction_qs=Transaction.objects.filter(created_date__month=cur_month,created_date__year=cur_year)
        total_income=transaction_qs.filter(type="income").values("amount").aggregate(total_income=Sum("amount"))
        total_expense=transaction_qs.filter(type="expenses").values("amount").aggregate(total_expense=Sum("amount"))
        category_summary=transaction_qs.values("category").annotate(total=Sum("amount"))
        # summary=[{dic.get("category"):dic.get("total")} for dic in category_summary]
        summary=list(category_summary)

        data={"total_income":total_income.get("total_income"),
              "total_expense":total_expense.get("total_expense"),
              "category_summary":summary
              }
        return Response(data=data)
  

