import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { MapObject, MapObjectType } from "./mapObject";
import { Observable } from "rxjs/Observable";

@Injectable()
export class MapService {
    private urlMap: Map<MapObjectType, string> = new Map<MapObjectType, string>();

    constructor(private http: Http) {
        this.initializeUrlMap();
    }

    public getMapObjects(type: MapObjectType): Observable<MapObject[]> {
        let requestUrl = this.urlMap.get(type);
        return this.http.get(requestUrl)
                        .map(this.extractData)
                        .catch(this.handleError);
    }

    private extractData(response: Response): MapObject[] {
        let data = response.json() || [];
        return <MapObject[]> data;
    }

    private handleError(error: any) {
        let errorMessage = "Server error";
        if (error.message) {
            errorMessage = error.message;
        } else if (error.status) {
            errorMessage = `${error.status} - ${error.statusText}`;
        }
        console.error(errorMessage);
        return Observable.throw(errorMessage);
    }

    private initializeUrlMap() {
        this.urlMap.set(MapObjectType.EVENTS, "api/events.json");
        this.urlMap.set(MapObjectType.FACEBOOK_PAGES, "api/facebook.json");
    }
}
