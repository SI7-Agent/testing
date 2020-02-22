import re
import enum

def get_suffix_str(suffix):
    string_res = ''
    for i in suffix:
        string_res += r'\b\w+' + i + r'\w*|'

    return string_res[:-1]

# suffix = ['чек', 'ецк', 'ишк', 'чк', 'очк', 'иц', 'урк', 'чик', 'ик', 'ушк', 'ок', 'ичк', 'еньк']
suffix = ['чек', 'ишк', 'чк', 'очк', 'иц', 'урк', 'чик', 'ик', 'ушк', 'ок', 'ичк', 'еньк']
suffix_str = r'[' + r'|\b\w+'.join(suffix) + r']'
suffix_str2 = r'|\b\w+'.join(suffix)
suffix_str3 = get_suffix_str(suffix)
# print(suffix_str3)

text = 'Котик мурлыкал от того, что его гладили по брюшку. ' \
       'Алиса закрепила на перилах мостика маленький замочек, где было написано её желание. ' \
       'Алёша отрезал кусочек пирога, который испекла бабушка. ' \
       'Маленьких синиц в домике не нашёл мальчик. ' \
       'Белочка грызла маленький орешек. Настя сплела для своей сестры милый веночек из полевых цветов. ' \
       'Выкинув ключик от свадебного замка, Андрей и Полина улыбнулись. ' \
       'Мама и папа наконец-то купили маленькому сыночку столик для игрушек.'

all_words = re.findall(r"\b\w+", text)

#################################################################################################
# for now doing automat

class Automat(enum.Enum):
    start = 0
    #########
    ch = 1
    ch_e = 2
    ch_e_k = 3
    ch_k = 4
    ch_i = 5
    ch_i_k = 6
    #########
    e = 7
    e_c = 8
    e_c_k = 9
    e_n = 10
    e_n_soft = 11
    e_n_soft_k = 12
    #########
    o = 13
    o_k = 14
    o_ch = 15
    o_ch_k = 16
    #########
    i = 17
    i_sh = 18
    i_sh_k = 19
    i_c = 20
    i_k = 21
    i_ch = 22
    i_ch_k = 23
    #########
    u = 24
    u_r = 25
    u_r_k = 26
    u_sh = 27
    u_sh_k = 28
    #########
    finish = 29

def check_words(word, automat):
    current_state = automat.start
    original_word = word
    return_flag = False
    a = 0
    word = word.lower()

    while a <= len(word):
        try:
            i = word[a]
        except:
            i = None
            pass

        # print(i)
        if current_state == automat.start:
            if i == 'ч' and a:
                current_state = automat.ch
            elif i == 'о' and a:
                current_state = automat.o
            elif i == 'у' and a:
                current_state = automat.u
            elif i == 'и' and a:
                current_state = automat.i
            elif i == 'е' and a:
                current_state = automat.e

        elif current_state != automat.finish:
            if current_state == automat.ch:
                if i == 'ч':
                    pass
                elif i == 'е':
                    current_state = automat.ch_e
                elif i == 'и':
                    current_state = automat.ch_i
                elif i == 'к':
                    current_state = automat.ch_k
                else:
                    current_state = automat.start
                    a -= 1

            elif current_state == automat.ch_e:
                if i == 'к':
                    current_state = automat.ch_e_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.ch_e_k:
                current_state = automat.finish

            elif current_state == automat.ch_k:
                current_state = automat.finish

            elif current_state == automat.ch_i:
                if i == 'к':
                    current_state = automat.ch_i_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.ch_i_k:
                current_state = automat.finish

            elif current_state == automat.o:
                if i == 'ч':
                    current_state = automat.o_ch
                elif i == 'к':
                    current_state = automat.o_k
                elif i == 'о':
                    pass
                else:
                    current_state = automat.start
                    a -= 1

            elif current_state == automat.o_k:
                current_state = automat.finish

            elif current_state == automat.o_ch:
                if i == 'к':
                    current_state = automat.o_ch_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.o_ch_k:
                current_state = automat.finish

            elif current_state == automat.u:
                if i == 'у':
                    pass
                elif i == 'р':
                    current_state = automat.u_r
                elif i == 'ш':
                    current_state = automat.u_sh
                else:
                    current_state = automat.start
                    a -= 1

            elif current_state == automat.u_r:
                if i == 'к':
                    current_state = automat.u_r_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.u_r_k:
                current_state = automat.finish

            elif current_state == automat.u_sh:
                if i == 'к':
                    current_state = automat.u_sh_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.u_sh_k:
                current_state = automat.finish

            elif current_state == automat.i:
                if i == 'ч':
                    current_state = automat.i_ch
                elif i == 'к':
                    current_state = automat.i_k
                elif i == 'ш':
                    current_state = automat.i_sh
                elif i == 'ц':
                    current_state = automat.i_c
                elif i == 'и':
                    pass
                else:
                    current_state = automat.start
                    a -= 1

            elif current_state == automat.i_sh:
                if i == 'к':
                    current_state = automat.i_sh_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.i_sh_k:
                current_state = automat.finish

            elif current_state == automat.i_c:
                current_state = automat.finish

            elif current_state == automat.i_k:
                current_state = automat.finish

            elif current_state == automat.i_ch:
                if i == 'к':
                    current_state = automat.i_ch_k
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.i_ch_k:
                current_state = automat.finish

            elif current_state == automat.e:
                if i == 'е':
                    pass
                # elif i == 'ц':
                #     current_state = automat.e_c
                elif i == 'н':
                    current_state = automat.e_n
                else:
                    current_state = automat.start
                    a -= 1

            # elif current_state == automat.e_c:
            #     if i == 'к':
            #         current_state = automat.e_c_k
            #     else:
            #         current_state = automat.start
            #         a -= 2
            #
            # elif current_state == automat.e_c_k:
            #     current_state = automat.finish

            elif current_state == automat.e_n:
                if i == 'ь':
                    current_state = automat.e_n_soft
                else:
                    current_state = automat.start
                    a -= 2

            elif current_state == automat.e_n_soft:
                if i == 'к':
                    current_state = automat.e_n_soft_k
                else:
                    current_state = automat.start
                    a -= 3

            elif current_state == automat.e_n_soft_k:
                current_state = automat.finish

        else:
            break

        # print(current_state)
        a += 1

    if current_state == automat.finish:
        # print("defined word is", original_word)
        return_flag = True
    # else:
    #     print()
    #     print("current state is", current_state)

    return return_flag

def find_suffixes(words, automat):
    res = []
    for i in words:
        if check_words(i, automat):
            res.append(i)

    return res

def check_expression():
    global all_words
    global res

    percentage = float(len(res)/len(all_words) * 100)

    if percentage <= 0:
        print('Текст эмоционально не окрашен')
    elif percentage <= 25:
        print('Текст эмоционально окрашен слегка')
    elif percentage <= 50:
        print('Текст эмоционально окрашен наполовину')
    elif percentage <= 75:
        print('Текст эмоционально окрашен больше половины')
    elif percentage <= 100:
        print('Текст эмоционально перекрашен')


# check_words("бабушка", Automat)
res = find_suffixes(all_words, Automat)
res2 = re.findall(suffix_str3, text)

print(res)
print(res2)
check_expression()