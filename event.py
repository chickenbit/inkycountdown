from datetime import date


class Event(object):
    """
    Event class for tracking annual date events
    """
    def __init__(self, name, event_date, event_type=r'birthday'):
        """

        :param name:
        :param event_date: date() object with mm/dd/yyyy.  date(dt.year, dt.month, dt.day)
        :param event_type: default to birthday
        """
        self.name = name
        self.date = event_date
        self.event_type = event_type

    def __repr__(self):
        return repr((self.name, self.date, self.event_type))

    def days_til_event(self):
        """
        How many days till the annual event
        :return: days till next annual event
        """
        today = date.today()
        next_birthday = date(today.year, self.date.month, self.date.day)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        time_to_birthday = abs(next_birthday - today)
        return time_to_birthday.days

    def will_be(self):
        """
        Age of the event in years
        :return:
        """
        # get current age, and add 1
        today = date.today()
        age_delta = today.year - self.date.year - ((today.month, today.day) < (self.date.month, self.date.day))
        will_be = age_delta + 1
#        agedelta2 = today - self.date
#        will_be2 = math.floor(agedelta2.days / 365 + 1)
#        will_be3 = self._findAge(today.day, today.month, today.year, (int)(self.date.day), (int)(self.date.month), int(self.date.year))
#        print("{}: AgeDelta 1: {}, AgeDelta 2: {} AgeDelta 3 {}, Diff {}".format(self.name, agedelta, will_be2, will_be3, agedelta - will_be2))
        return will_be

    def _findAge(self, current_day, current_month, current_year, birth_day, birth_month, birth_year):

        # if birth date is greater then current birth_month
        # then donot count this month and add 30 to the date so
        # as to subtract the date and get the remaining days

#        month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (birth_day > current_day):
            current_month = current_month - 1
#            current_date = current_date + month[birth_month - 1]

            # if birth month exceeds current month, then
        # donot count this year and add 12 to the
        # month so that we can subtract and find out
        # the difference
        if (birth_month > current_month):
            current_year = current_year - 1
#            current_month = current_month + 12

        # calculate date, month, year
#        calculated_date = current_date - birth_date
#        calculated_month = current_month - birth_month
        calculated_year = current_year - birth_year
        return calculated_year
