from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, JobSerializer
from joblistingapp.models import Job as job

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
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        jobs = job.objects.all()
        if not jobs.exists():
            return Response({'error': 'No jobs found'}, status=status.HTTP_204_NO_CONTENT)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

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
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
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
