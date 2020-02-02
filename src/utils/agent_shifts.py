
weekdays = ['MONDAY', "TUESDAY", "WEDNESDAY",
            "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def agent_shifts_value_to_human_readable_value(workTimings):
    if (workTimings and len(workTimings.keys())):
        return workTimings.get('start') + " to " + workTimings.get('end')
    return ""


def get_weekday(weekday_number):
    if not weekday_number:
        return ""
    return weekdays[weekday_number]
