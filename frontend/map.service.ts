import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { MapObject } from "./mapObject";
import { Observable } from "rxjs/Observable";

@Injectable()
export class MapService {
    constructor(private http: Http) {}

    private mapObjectsUrl = "api/mapobjects.json";

    getMapObjects(): Observable<MapObject[]> {
        return this.http.get(this.mapObjectsUrl)
                        .map(this.extractData)
                        .catch(this.handleError);
    }

    private extractData(response: Response) {
        let data = response.json() || [];
        return <MapObject[]>data;
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
}
