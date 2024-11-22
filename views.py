from django.shortcuts import render, redirect
from .forms import BankDetailsForm
from .models import BankDetails
import pandas as pd
from django.core.cache import cache  # Import Django's cache system

def add_bank_details(request):
    if request.method == 'POST':
        form = BankDetailsForm(request.POST)
        if form.is_valid():
            bank_details = form.save(commit=False)
            bank_details.bank_rule_mapping = None  # Initially null
            bank_details.save()
            return redirect('bank_details_list')  # Redirect to a list view or a success page
    else:
        form = BankDetailsForm()
    
    return render(request, 'add_bank_details.html', {'form': form})




def bank_details_list(request):
    bank_details = BankDetails.objects.all()  # Fetch all bank details for the table
    bank_names = BankDetails.objects.values_list('bank_name', flat=True).distinct()  # Get all unique bank names

    # Try to fetch column names and total columns from cache
    column_names = cache.get('column_names')
    total_columns = cache.get('column_total', 0)  # Default total_columns to 0 if not cached

    if request.method == 'POST' and 'uploaded_file' in request.FILES:
        uploaded_file = request.FILES['uploaded_file']

        # Use pandas to read the file temporarily and extract column headers
        try:
            # Check the file extension to determine the appropriate pandas reader
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension in ['xls', 'xlsx', 'ods']:
                df = pd.read_excel(uploaded_file, engine='openpyxl' if file_extension == 'xlsx' else None)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")

            column_names = df.columns.tolist()
            total_columns = len(column_names)  # Calculate total columns

            # Cache the column names and total column count for 2 minutes (120 seconds)
            cache.set('column_names', column_names, timeout=120)
            cache.set('column_total', total_columns, timeout=120)
        except Exception as e:
            column_names = [f"Error reading file: {e}"]
            total_columns = 0

    return render(request, 'bank_details_list.html', {
        'bank_details': bank_details,
        'column_names': column_names,  # Pass cached column names to the template
        'total_columns': total_columns,  # Pass cached total column count to the template
        'bank_names': bank_names,  # Pass the list of bank names
    })
