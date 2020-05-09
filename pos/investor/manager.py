from django.db import models, transaction, DatabaseError
from django.db.models import Prefetch, Sum, F, Value
from django.db.models.functions import Coalesce


class InvestorHistory(object):
    pass


class InvestorManager(models.Manager):
    def all_investor(self):
        data = self.model.objects.prefetch_related('investor_history').annotate(
            total_invest=Coalesce(Sum(F('investor_history__amount')), Value(0)))
        return data

    @transaction.atomic
    def create_investor(self, investor_data):
        try:
            new_investor = self.model(name=investor_data['name'], phone_no=investor_data['phone_no'],
                                      address=investor_data['address'])
            new_investor.save(using=self.db)
            from investor.models import InvestHistory
            invest = InvestHistory(share_holder=new_investor, amount=investor_data['amount'])
            invest.save(using=self.db)
        except DatabaseError as e:
            raise DatabaseError("Technical problem to create investor")
        return new_investor

    @transaction.atomic
    def release_investor(self, id):
        try:
            investor = self.model.objects.filter(id=id).prefetch_related('investor_history').annotate(
                total_invest=Coalesce(Sum(F('investor_history__amount')), Value(0))).first()
            from investor.models import ShareHolderReleaseHistory
            release_investor = ShareHolderReleaseHistory(joining_date=investor.joining_date, name=investor.name,
                                                         phone_no=investor.phone_no, address=investor.address,
                                                         total_investment=investor.total_invest)
            release_investor.save(using=self.db)
            investor.delete()
        except DatabaseError as e:
            raise DatabaseError("Technical problem to releasing shareholder")

        return True
