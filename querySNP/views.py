import itertools
from django.conf import settings
import datetime
import os
from enum import Enum
from functools import reduce
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView, DetailView, TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from .forms import QuerySNP
from .models import snpsAssociated_FDR_chrom, snpsAssociated_FDR_chr_table

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2


class SNPAssociated(TemplateView):
    template = 'querySNP.html'

    def get(self, request):  
        form = QuerySNP()
        return render(request, self.template, {
            'query_form': form
        })

    def post(self, request):
        form = QuerySNP(request.POST)
        error = None
        snpInfo = {}
        associations = []

        if form.is_valid():
            snpId = form.cleaned_data.get('SNPid')
            if snpId is not '':
                snpInfo = snpsAssociated_FDR_chrom.get_SNP_chrom(snpId)

                if snpInfo is None:
                    error = Errors.NOT_ASSOCIATED
                else:
                    associations = snpsAssociated_FDR_chr_table(snpInfo.chrom).get_Associated(snpInfo.snpID)

        else:
            error = Errors.NOT_VALID

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'associations': associations,
            'query_form': form,
            'error': error,
            'reference': associations[0].refBase if len(associations) > 0 else None,
            'alternative': associations[0].altBase if len(associations) > 0 else None,
            'position': associations[0].chromStartSNP if len(associations) > 0 else None
        })   