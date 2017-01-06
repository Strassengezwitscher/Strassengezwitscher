export class Helper {

    public static dateToYMD(date: Date): string {
        return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    }

    public static subtract30Days(date: Date): Date {
        const secondsOfADay = 86400;
        const msOfADay = secondsOfADay * 1000;

        return new Date(date.getTime() - 30 * msOfADay);
    }

    public static dayLeadingZero(date: Date): string {
        return ("0" + date.getDate()).slice(-2);
    }

    public static monthLeadingZero(date: Date): string {
        return ("0" + (date.getMonth() + 1)).slice(-2);
    }

    public static regionalDateFormat(date: Date) {
        return `${Helper.dayLeadingZero(date)}.${Helper.monthLeadingZero(date)}.${date.getFullYear()}`;
    }

    public static nextDay(date: Date): Date {
        let nextDay = new Date(date);
        nextDay.setDate(nextDay.getDate() + 1);

        return nextDay;
    }
}
