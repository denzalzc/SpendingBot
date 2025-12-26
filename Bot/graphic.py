import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
from models import ExpenseCategory
from io import BytesIO


all_categories = [c.value for c in ExpenseCategory]


def create_diag(categories, sum_of_category):
    data = {
        'Indicator': categories,
        'Spends': sum_of_category
        }
        
    df = pd.DataFrame(data)
    df.plot.pie(y='Spends', labels=df['Indicator'], autopct='%1.1f%%', startangle=90)
    plt.axis('equal')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    result = buffer.getvalue()
    buffer.close()


    return result
