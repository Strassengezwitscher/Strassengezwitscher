export class MapObject {
    public id: number;
    public name: string;
    public locationLong: number;
    public locationLat: number;
    public date: Date;
    public iconPath: string;
    public iconSelectedPath: string;
    public opacity: number;
}

export enum MapObjectType {
    EVENTS = 0,
    FACEBOOK_PAGES,
}

export enum MapStateType {
    VIEWING = 0,
    ADDING,
}
