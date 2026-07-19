from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from .forms import StudentForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required(login_url='/login/')
def student_list(request):
    return render(request, 'students/list.html')

def add_student(request):
    pass


@login_required(login_url='/login/')
def view_students(request):

    if request.user.is_superuser:
        students = Student.objects.all()
        total_students = Student.objects.count()
        my_students = Student.objects.count()
    else:
        students = Student.objects.filter(created_by=request.user)
        total_students = Student.objects.count()
        my_students = Student.objects.filter(created_by=request.user).count()

    context = {
        "students": students,
        "total_students": total_students,
        "my_students": my_students,
    }

    return render(request, "students/view_students.html", context)


@login_required(login_url='/login/')
def view_student(request, id):

    student = get_object_or_404(Student, id=id)

    if not request.user.is_superuser and student.created_by != request.user:
        messages.error(request, "❌ You are not authorized to view this student.")
        return redirect('view_students')

    return render(request, 'students/view_student.html', {'student': student})


# 📌 Add student
@login_required(login_url='/login/')
def add_student(request):
    form = StudentForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            student = form.save(commit=False)
            student.created_by = request.user
            student.save()

            messages.success(request, "Student added successfully ✔")
            return redirect('view_students')

    return render(request, "students/add_students.html", {"form": form})


# 📌 Update student
@login_required(login_url='/login/')
def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully ✔")
            return redirect('view_students')

    return render(request, "students/update_students.html", {"form": form})


# 📌 Delete student
@login_required(login_url='/login/')
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully ✔")
        return redirect('view_students')

    return render(request, "students/delete_students.html", {"student": student})

from django.db.models import Q  # 👈 हे फाईलच्या अगदी वर इम्पोर्ट करा (खूप महत्त्वाचे!)

@login_required(login_url='/login/')
def search_student(request):
    query = request.GET.get('q', '')  # HTML मधून 'q' ची व्हॅल्यू (टाईप केलेलं नाव) घेईल
    students = []
    
    if query:
        # विद्यार्थ्याचे नाव, ईमेल किंवा कोर्स यांपैकी कशामध्येही तो शब्द असेल तर फिल्टर करेल
        students = Student.objects.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(course__icontains=query)
        )
    else:
        # जर सर्च बॉक्स रिकामा असेल, तर कोणतेच विद्यार्थी दिसणार नाहीत (किंवा Student.objects.all() लिहू शकता)
        students = []

    # गोळा केलेला डेटा पुन्हा HTML कडे पाठवतोय
    return render(request, 'students/search.html', {'students': students, 'query': query})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(request, "Account created successfully! Please login.")
            return redirect("login")

    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})

@login_required(login_url='/login/')
def dashboard(request):

    if request.user.is_superuser:
        total_students = Student.objects.count()
        my_students = Student.objects.count()
    else:
        total_students = Student.objects.count()
        my_students = Student.objects.filter(created_by=request.user).count()

    context = {
        "total_students": total_students,
        "my_students": my_students,
    }

    return render(request, "students/dashboard.html", context)