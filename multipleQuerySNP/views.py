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

from .forms import MultipleQuerySNP
from .models import snpsAssociated_FDR_chrom, snpsAssociated_FDR_chr_table, snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights, getSNPID

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

class SNPAssociated(TemplateView):
    template = 'multipleQuerySNP.html'

    def get(self, request):  
        form = MultipleQuerySNP()
        return render(request, self.template, {
            'query_form': form
        })

    def post(self, request):
        form = MultipleQuerySNP(request.POST)
        error = None
        snpInfo = []
        associations = []
        genes = []
        enhancers = []
        tLights = []
        errors={}
        baseLinkGene = settings.SUB_SITE+"/queryGene/gene/"
        baseLinkSNP = settings.SUB_SITE+"/querySNP/snp/"

        snpsQueried = {}
        if form.is_valid():
            snpIds = form.cleaned_data.get('SNPids').replace("\r","").replace(" ","").split("\n")
            if snpIds is not '':
                for snpId in snpIds:
                    if snpId:
                        if not 'rs' in snpId:
                            error = Errors.NOT_VALID
                            errors[snpId] = error
                            continue
                        snpInfoSNP = snpsAssociated_FDR_chrom.get_SNP_chrom(snpId)
                        try:
                            snpsQueried[snpId]
                            continue
                        except:
                            snpsQueried[snpId] = True
                            snpInfo.append(snpInfoSNP)
                        if snpInfoSNP is None:
                            checkid = getSNPID.get_SNP(snpId)
                            if checkid!=None:
                                error = Errors.NOT_ASSOCIATED
                                errors[snpId] = error
                                snpsQueried[snpId]=False
                            else:
                                error = Errors.NOT_VALID
                        else:  
                            #associationsSNP = snpsAssociated_FDR_chr_table(snpInfoSNP.chrom).get_Associated(snpInfoSNP.snpID)
                            #associations.append(associationsSNP)
                            genesSNP = snpsAssociated_FDR_promotersEPD.get_Promoters(snpId)
                            # Añado a genes el count
                            genesNew = []
                            for gene in genesSNP:
                                info = {
                                    'data': gene[1],
                                    'count': gene[0],
                                    'distance':abs(gene[1].chromStartPromoter-snpInfoSNP.chromStart)
                                }
                                genesNew.append(info)
                            genes.append(genesNew)
                        
                            enhancersSNP = snpsAssociated_FDR_enhancers.get_Enhancers(snpId)
                            enhancers.append(enhancersSNP)

                            tLightsSNP = snpsAssociated_FDR_trafficLights.get_trafficLights(snpId)
                            tLights.append(tLightsSNP)
            else:
                error = Errors.NOT_VALID
                errors[snpId] = error

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'associations': associations,
            'genes': genes,
            'enhancers':enhancers,
            'tLights':tLights,
            'baseLinkSNP':baseLinkSNP,
            'baseLinkGene':baseLinkGene,
            'query_form': form,
            'errors': errors
        }) 