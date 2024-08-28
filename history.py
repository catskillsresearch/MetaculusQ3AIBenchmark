history = { '08JUL24': [25876, 25877, 25875, 25873, 25871, 25878, 25874, 25872],
            '09JUL24': [26006, 25936, 25935, 25934, 25933, 26004, 26005],
            '10JUL24': [25955, 25956, 25957, 25960, 25959, 25954, 25953, 25952, 25958],
            '11JUL24': [26019, 26018, 26017, 26020, 26022, 26021, 26023, 26024],
            '12JUL24': [26095, 26096, 26097, 26098, 26099, 26100, 26101, 26102],
            '15JUL24': [26133, 26134, 26138, 26139, 26140, 26157, 26158, 26159],
            '16JUL24': [26189, 26190, 26191, 26192, 26193, 26194, 26195, 26196],
            '17JUL24': [26210, 26211, 26212, 26213, 26214, 26215, 26216],
            '18JUL24': [26232, 26233, 26234, 26235, 26236],
            '19JUL24': [26302, 26303, 26304, 26305, 26306, 26307],
            '22JUL24': [26387, 26388, 26389, 26390, 26391, 26392],
            '23JUL24': [26404, 26405, 26406, 26407, 26408],
            '24JUL24': [26550, 26551, 26552, 26553, 26554, 26555],
            '25JUL24': [26568, 26569, 26570, 26571, 26572, 26573, 26574, 26575, 26576, 26577],
            '26JUL24': [26638, 26639, 26640, 26641, 26642, 26643, 26644, 26645, 26646],
            '29JUL24': [26665, 26666, 26667, 26668, 26669, 26670, 26671, 26683],
            '30JUL24': [26700, 26701, 26702, 26703, 26704, 26705, 26706],
            '31JUL24': [26816, 26817, 26818, 26819, 26820, 26821, 26844],
            '01AUG24': [26771, 26772, 26773, 26774, 26775, 26776, 26777, 26778, 26779, 26780, 26781],
            '02AUG24': [26837, 26838, 26839, 26840, 26841, 26842],
            '05AUG24': [26913, 26914, 26915, 26916, 26917, 26918, 26919, 26920],
            '06AUG24': [26957, 27019, 27020, 27021, 27022],
            '07AUG24': [26958, 26959, 27017, 27018],
            '08AUG24': [26975, 26976, 26977, 26978, 26979, 26980, 26981, 26982, 26983, 26984, 26985, 26986, 27039],
            '09AUG24': [27085, 27086, 27087, 27088, 27089],
            '10AUG24': [27132, 27133, 27134, 27135, 27136],
            '13AUG24': [27137, 27138, 27140, 27141],
            '14AUG24': [27157, 27158, 27159, 27160, 27161, 27200, 27219, 27220, 27221, 27222, 27223],
            '15AUG24': [27248, 27249],
            '16AUG24': [27238, 27239, 27240, 27241],
            '19AUG24': [27258, 27259, 27260, 27261, 27262, 27263],
            '20AUG24': [27277, 27278, 27279, 27280, 27281, 27282, 27283],
            '21AUG24': [27446, 27521, 27522, 27523, 27524],
            '22AUG24': [27447, 27484, 27485, 27486, 27487, 27488, 27489, 27490, 27491, 27492, 27493, 27538, 27539],
            '23AUG24': [27515, 27545, 27546, 27547, 27548, 27576, 27581, 27582, 27583, 27584],
            '26AUG24': [27602, 27603, 27604, 27605, 27606, 27607, 27608, 27609, 27610],
            '27AUG24': [27637, 27638, 27639, 27640],
            '28AUG24': [27720, 27721, 27722, 27723, 27732, 27733]}

if __name__=="__main__":
    from metaculus import get_question_details
    import os, json, datetime
    from tqdm import tqdm
    import time
    os.makedirs('questions', exist_ok=True)
    for key in tqdm(history):
        for qid in tqdm(history[key]):
            ifp = get_question_details(qid)
            fn = f'questions/{qid}.json'
            with open(fn, 'w') as f:
                json.dump(ifp, f)
                print('saved', fn)
        time.sleep(2)