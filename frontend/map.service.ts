import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { MapObject } from "./mapObject";
import { Observable } from "rxjs/Observable";

@Injectable()
export class MapService {
    constructor(private http: Http) {}

    private mapObjectsUrl = "api/mapobjects/?format.json";

    getMapObjects(): Observable<MapObject[]> {
        return this.http.get(this.mapObjectsUrl)
                        .map(this.extractData)
                        .catch(this.handleError);
    }

    private extractData(res: Response) {
        let data = res.json() || [];
        return <MapObject[]>data;
    }

    private handleError(error: any) {
        let errMsg = (error.message) ? error.message : error.status ? `${error.status} - ${error.statusText}` : 'Server error';
        console.error(errMsg); // log to console instead
        return Observable.throw(errMsg);
    }
}
