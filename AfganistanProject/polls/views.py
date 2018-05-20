from django.shortcuts import render
from polls.forms import SearchInDbForm
from django.http import HttpResponseRedirect
from biohackProject.Retriever.Retriever import Retriever
import json
from polls.models import AlignmentNode
from polls.models import FastaData
import os
import uuid
from polls.Tools import MyTools
from django.core import serializers
from biohackProject.TreeDrawer.TreeDrawer import TreeDrawer


def index(request):
    template_name = "polls/index.html"
    form = SearchInDbForm()
    context = {
        'searchingForm': form
    }
    return render(request, template_name, context)


def get_data_from_db(request):
    print(request)
    context = {}
    if request.method == 'POST':
        form = SearchInDbForm(request.POST)
        if form.is_valid():

            # splitted indexes from input
            splitted_data = form.cleaned_data['index_for_req'].split(";")
            for i, v in enumerate(splitted_data):
                splitted_data[i] = v.strip()
            print(splitted_data)
            # retriver data
            ret = Retriever()
            res_dict = ret.retrieve_blast_data(gi=splitted_data, filename="example.fasta", n=50)

            # draw tree
            file_name = uuid.uuid4().__str__()
            TreeDrawer().draw_tree(file_name)

            # alignment.aln parse
            alignment = MyTools.parse_alignment("alignment.aln")
            results = [ob.as_json() for ob in alignment]

            test = json.dumps(results)
            # add objects to session
            request.session['file_name'] = file_name
            request.session['splittedData'] = splitted_data
            request.session['alignment_data'] = json.dumps(results)
            return HttpResponseRedirect("/polls/result")
        else:
            print("not valid")
    else:
        form = SearchInDbForm()

    return render(request, "polls/index.html", context)


def result(request):
    file_name = request.session.get('file_name')
    splitted_data = request.session.get('splittedData')
    alignment_data = json.loads(request.session.get('alignment_data'))
    final_data = []

    for item in alignment_data:
        final_data.append(AlignmentNode(item['input_label'], item['input_value']))

    context = {
        'file_path': 'images/' + file_name + '.png',
        'splitted_data': splitted_data,
        'alignment_data': final_data
    }
    return render(request, "polls/result.html", context)
