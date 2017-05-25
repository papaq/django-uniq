import itertools

from django.db.models import Q

from channels.models import University, Faculty, Group


def university_search_helper(count, query):
    result_list = University.objects.filter(Q(title__icontains=query) | Q(short_titles__icontains=query))
    return result_list[:count]


def faculty_search_helper(count, query, university_pk):
    university = University.objects_safe.safe_get(pk=university_pk)
    if not university:
        return []
    result_list = university.faculties.filter(title__icontains=query)
    return result_list[:count]


def group_search_helper(count, query, faculty_pk):
    faculty = Faculty.objects_safe.safe_get(pk=faculty_pk)
    if not faculty:
        return []
    model_list = Group.objects.filter(group_stack__faculty=faculty, title__icontains=query)
    return model_list[:count]


def _university_search_helper(count, query):
    model_list = University.objects.filter(title__icontains=query)
    words = query.split(' ')
    for L in range(1, count + 1):
        for subset in itertools.permutations(words, L):
            count1 = 1
            query1 = subset[0]
            while count1 != len(subset):
                query1 = query1 + " " + subset[count1]
                count1 += 1
            model_list = University.objects.filter(title__icontains=query1)
    return model_list.distinct()


def _faculty_search_helper(count, query):
    model_list = Faculty.objects.filter(title__icontains=query)
    words = query.split(' ')
    for L in range(1, count + 1):
        for subset in itertools.permutations(words, L):
            count1 = 1
            query1 = subset[0]
            while count1 != len(subset):
                query1 = query1 + " " + subset[count1]
                count1 += 1
            model_list = Faculty.objects.filter(title__icontains=query1)
    return model_list.distinct()


def _group_search_helper(count, query):
    model_list = Group.objects.filter(title__icontains=query)
    words = query.split(' ')
    for L in range(1, count + 1):
        for subset in itertools.permutations(words, L):
            count1 = 1
            query1 = subset[0]
            while count1 != len(subset):
                query1 = query1 + " " + subset[count1]
                count1 += 1
            model_list = Group.objects.filter(title__icontains=query1)
    return model_list.distinct()
