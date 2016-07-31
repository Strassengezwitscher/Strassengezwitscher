export class MapObject {
    public id: number;
    public name: string;
    public active: boolean;
    public location: string;
    public locationLong: number;
    public locationLat: number;
}

export enum MapObjectType {
            EVENTS = 0,
            FACEBOOK_PAGES
}
