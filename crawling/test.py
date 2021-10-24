finn_td = '''
<td class="">
                                                                                                 8.29

                                                        </td>
'''

finn_td_str = finn_td.replace(" ","").replace("\n","").split(">")[1].split("<")[0]
print(finn_td_str)