export class Helper {

    public static dateToYMD(date: Date): string {
        return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    }

    public static subtract30Days(date: Date) {
        const secondsOfADay = 86400;
        const msOfADay = secondsOfADay * 1000;

        return new Date(date.getTime() - 30 * msOfADay);
    }
}
