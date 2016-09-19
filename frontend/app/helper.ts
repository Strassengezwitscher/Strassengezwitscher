export class Helper {

    public static dateToYMD(date: Date): string {
        return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    }

}
