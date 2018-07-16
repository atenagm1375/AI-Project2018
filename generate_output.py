from file_decode import *


def generate_output(ans):
    writer = pd.ExcelWriter('./result report/result_' + str(skill_filenum) + '_' + str(free_time_filenum) + '_' +
                            str(free_class_filenum) + '_' + str(capacity_filenum) + '_' + str(register_filenum) +
                            '.xlsx')
    df = {}
    for p in profs_list:
        df[p] = pd.DataFrame(index=days, columns=times, data='-')

    for i in range(ans.size // 2):
        gene1 = ans[i]
        gene2 = ans[i + ans.size // 2]
        if gene1 != -1:
            prof = ans.get_gene_prof(i)
            cls = ans.get_gene_class(i)
            day_time = gene1 % timeslots_num
            data = courses_list[i].split('-')[0] + '-' + cls
            df[prof].iat[day_time % len(days), day_time // len(days)] = data
        if gene2 != -1:
            prof = ans.get_gene_prof(i + ans.size // 2)
            cls = ans.get_gene_class(i + ans.size // 2)
            day_time = gene2 % timeslots_num
            data = courses_list[i].split('-')[0] + '-' + cls
            df[prof].iat[day_time % len(days), day_time // len(days)] = data

    for p in profs_list:
        df[p].to_excel(writer, sheet_name=p)
    writer.save()
