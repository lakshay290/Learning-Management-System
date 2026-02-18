
from django.shortcuts import render,get_object_or_404
from courses.models import Enrollment
def generate_certificate(request,id):
    enroll=get_object_or_404(Enrollment,id=id)
    return render(request,'certificate.html',{'enroll':enroll})
