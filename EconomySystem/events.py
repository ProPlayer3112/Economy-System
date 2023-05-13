"""
YOU CAN ADD AS MUCH EVENTS AS YOU WANT
This are the text's that will be sent when you use the Commands!
"""


def workP(coins, eco):

    eventPositive = [
            f'Du hast gut gearbeitet und erhältst {eco} **{coins}** Diamanten!',
            f'Du hast einen Kuchen gebacken und erhältst {eco} **{coins}** Diamanten!',
            f'Du hast ein paar Kekse gebacken und jemand hat sie gekauft. Er/Sie bezahlte {eco} **{coins}** Diamanten!',
            f'Du hast ein paar Autos gewaschen und erhältst {eco} **{coins}** Diamanten!',
            f'Du hast ein paar Codes verkauft und verdienst {eco} **{coins}** Diamanten!',
            f'Sie arbeiten heute hart im Büro, aber anstatt befördert zu werden, verdienen Sie {eco} **{coins}** Diamanten! Schön.',
            f'Unser Chef war heute nett und hat dir {eco} **{coins}** Diamanten geschenkt!',
            f'Du hast eine gute Note, also hat deine Mutter beschlossen, dir {eco} **{coins}** Diamanten zu geben!',
            f'Jemand hat {eco} **{coins}** Diamanten in deinem Livestream gespendet! Gut gemacht.',
            f'Du hast einige Items verkauft und {eco} **{coins}** Diamanten verdient!',
            f'Du arbeitest als Bauer und verdienst {eco} **{coins}** Diamanten!',
            f'Du fängst einen Fisch und gibst ihn deinem besten Freund. Er zahlt dir {eco} **{coins}** Diamanten für einen guten Job!',
            f'Du arbeitest in einem Restaurant und hast ein Trinkgeld von {eco} **{coins}** Diamanten für einen guten Job bekommen!',
            f'Du gewinnst einen Burger-Wettessen. Der Preis sind {eco} **{coins}** Diamanten!',
            f'Du arbeitest als Polizist und verdienst {eco} **{coins}** Diamanten!'
        ]

    return eventPositive


def workN(coins, eco):

    eventNegative = [
            f'Du hast schlecht gearbeitet und verlierst {eco} **{coins}** Diamanten!'
        ]

    return eventNegative


def slutP(coins, eco):

    eventPositive = [
            f'Du hast einen guten Job gemacht und verdienst {eco} **{coins}** Diamanten!'
        ]

    return eventPositive


def slutN(coins, eco):

    eventNegative = [
            f'Die Frau von nebenan hat dich verarscht und dir das Portemonnaie gestohlen! Du verlierst {eco} **{coins} Diamanten**!'
        ]

    return eventNegative



def crimeP(coins, eco):

    eventPositive = [
            f'Du hast erfolgreich eine Bank überfallen und die Beute beträgt {eco} **{coins}** Diamaten!'
        ]

    return eventPositive


def crimeN(coins, eco):

    eventNegative = [
            f'Die Polizei hat dich beim überfallen einer Bank geschnappt und du musst {eco} **{coins}** Diamaten zahlen!'
        ]

    return eventNegative


def RobP(coins, eco):

    eventPositive = [
            f"Du hast die Brieftasche eines alten Mannes gestohlen und {eco} **{coins}** Diamanten herausgenommen!"
        ]

    return eventPositive


def RobN(coins, eco):

    eventNegative = [
            f'Du wurdest von einem Polizisten erwischt! Du musstest {eco} **{coins}** Diamanten bezahlen, um aus dem Gefängnis zu kommen!',
            f'Du hast versucht, einer alten Frau das Telefon zu stehlen, aber du wusstest nicht, dass sie ein Boxprofi ist! Sie schlug dir ins Gesicht und rief die Polizei. Du hast {eco} **{coins}** Diamanten bezahlt, um rauszukommen!'
        ]

    return eventNegative

def buyP(coins, eco):

    eventPos = [
            f'Du hast erfolgreich die Rolle Bettler gekauft.(Dadurch hast du nun {eco} **{coins}** Diamanten weniger)'
        ]

    return eventPos