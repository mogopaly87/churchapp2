from django.core.management.base import BaseCommand, CommandError
from Tax.models import Tithely
import pandas as pd

class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tithely = Tithely

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='csv file')

    def handle(self, *args, **options):
        file = options['file']
        df = pd.read_csv(file, sep=',')
        df.columns = ['net_amount', 'fees', 'amount', 'cover_fee', 'first_name',
                'last_name', 'giving_type', 'deposit_date', 'trans_date']
        df_new = df[['net_amount', 'first_name', 'last_name', 'giving_type', 'trans_date']]
        df_new.net_amount.apply(str)
        df_new.dropna(inplace=True)
        df_new['net_amount'] = df_new['net_amount'].map(lambda x: x.lstrip('$'))
        df_new2 = df_new.astype({'net_amount':'float'})
        df_new2 = df_new2.astype({'trans_date':'datetime64'})

        givings = []
        for i in range(len(df_new2)):
            givings.append(
                self.tithely(
                    net_amount = df_new2.iloc[i][0],
                    first_name = df_new2.iloc[i][1],
                    last_name = df_new2.iloc[i][2],
                    giving_type = df_new2.iloc[i][3],
                    trans_date = df_new2.iloc[i][4]
                )
            )
        self.tithely.objects.bulk_create(givings)