from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, JobSerializer
from joblistingapp.models import Job as job
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
class JobsPagination(PageNumberPagination):
    max_page_size=100
    page_size_query_param='page_size'
    page_size=5
    

class CreateJob(APIView):
    """
    API endpoint for managing job creation and retrieval for an authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all jobs created by the authenticated user.
        """
        jobs = job.objects.filter(user=request.user)
        paginator = JobsPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request):
        """
        Create a new job with data provided by the user.
        """
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Jobs(APIView):
    """
    API endpoint for retrieving and creating job listings.
    """
    def get(self, request):
        """
        Retrieve all job listings in the system.
        """
        query=request.GET.get('q', '')
        print(query)
        if query:
            jobs=job.objects.filter(Q (title__icontains=query)|Q (companyname__icontains=query))
        else:
            jobs=job.objects.all()
            if not jobs.exists():
                return Response({'error': 'No job found'}, status=status.HTTP_204_NO_CONTENT)
        jobs=jobs.order_by('id')
        paginator = JobsPagination()
        paginated_jobs = paginator.paginate_queryset(jobs, request)
        serializer = JobSerializer(paginated_jobs, many=True)
        return Response(serializer.data ,status=status.HTTP_200_OK)
        

    def post(self, request):
        """
        Create a new job listing.
        """
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):
    """
    API endpoint for user registration.
    """
    def post(self, request):
        """
        Create a new user account.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """
    API endpoint for user login.
    """
    def post(self, request):
        """
        Authenticate a user and return their details upon successful login.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            access_token = serializer.validated_data['access']

            # Set token in HttpOnly cookie
            response = JsonResponse({'message': 'Login successful!'})
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Lax'
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyJobs(APIView):
    """
    API endpoint for retrieving jobs associated with a specific company.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Retrieve all jobs for a specific company by its ID.
        """
        jobs = job.objects.filter(id=id)
        if not jobs.exists():
            return Response({'error': 'No jobs found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Job(APIView):
    """
    API endpoint for retrieving, updating, and deleting a specific job.
    """
    def get(self, request, id):
        """
        Retrieve details of a specific job by its ID.
        """
        job_instance = get_object_or_404(job, id=id)
        serializer = JobSerializer(job_instance)
        return Response(serializer.data)

    def patch(self, request, id):
        """
        Partially update a specific job by its ID.
        """
        job_instance = get_object_or_404(job, id=id)
        serializer = JobSerializer(job_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete a specific job by its ID.
        """
        job_instance = get_object_or_404(job, id=id)
        job_instance.delete()
        return Response({'success': 'Job deleted'}, status=status.HTTP_204_NO_CONTENT)
