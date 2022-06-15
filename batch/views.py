from django.shortcuts import render

from create_exam.models import Batch


def batch_detail(request, batch_id):
    batch = Batch.objects.get(id=batch_id)
    params = {
        'batch': batch,
    }
    return render(request, 'create-exam/batch/batch-detail.html', params)
