import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from pdf2docx import Converter
from .models import ConvertedFile
import uuid
from django.contrib.auth import login, authenticate
from .models import LoginForm
from .models import UserRegistrationForm



def generate_short_code():
    return str(uuid.uuid4())[:5]


@require_POST
def pdftoword(request):
    file = request.FILES.get('pdf_file')
    if file and file.name.endswith('.pdf'): 
        short_code = generate_short_code()
        converted_file = ConvertedFile(pdf_file=file, short_code=short_code)
        converted_file.save()


        filename = os.path.splitext(file.name)[0]
        docx_filename = filename.replace(" ", "_")
        docx_file_path = os.path.join(settings.MEDIA_ROOT, 'docx_files', docx_filename + '.docx')


        try:
            pdf_converter = Converter(converted_file.pdf_file.path, docx_file_path)
            pdf_converter.convert()

            converted_file.docx_file.name = os.path.join('pdf_files', docx_filename + '.docx')  # Add '.docx' extension here
            converted_file.save()

            return JsonResponse({'short_code': short_code})
        except Exception as e:
            return HttpResponse('Conversion failed or file not found', status=500)
    else:
        return HttpResponse('Invalid PDF file provided', status=400)

def convert_form(request):
    return render(request, 'index.html')

def downloadpage(request, pk):
    converted_file = ConvertedFile.objects.get(short_code=pk)
    d = os.path.splitext(converted_file.docx_file.name)[0]
    prefix_to_remove = "pdf_files\\"
    if d.startswith(prefix_to_remove):
        d = d[len(prefix_to_remove):]
    print(d)
    return render(request, 'dq.html', {'hi': converted_file,'h':d})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Kiểm tra xem username và password có hợp lệ không
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                # Đây là tài khoản admin, chuyển hướng đến trang admin
                login(request, user)
                return redirect('admin:index')
            else:
                # Đây là tài khoản user, chuyển hướng đến trang convert_form
                login(request, user)
                return redirect('convert_form')
        else:
            # Xử lý trường hợp đăng nhập không thành công, ví dụ: hiển thị thông báo lỗi
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})