# created by 2021/4/1 16:35
#配置公共模板变量
#LoginForm成为公共的模板变量
from .forms import LoginForm

def login_modal_form(request):
    return {'login_modal_form':LoginForm()}