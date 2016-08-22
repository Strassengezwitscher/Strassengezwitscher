export class MapObject {
    public id: number;
    public name: string;
    public locationLong: number;
    public locationLat: number;
}

export enum MapObjectType {
            EVENTS = 0,
            FACEBOOK_PAGES
}
