import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { DateFilter } from "./map.component";
import { MapObject, MapObjectType } from "./mapObject.model";

import { Helper } from "../helper";
import { Observable } from "rxjs/Observable";

@Injectable()
export class MapService {
    private urlMap: Map<MapObjectType, Map<DateFilter, string>> = new Map<MapObjectType, Map<DateFilter, string>>();

    constructor(private http: Http) {
        this.initializeUrlMap();
    }

    public getMapObjects(type: MapObjectType, dateFilter: DateFilter): Observable<MapObject[]> {
        let requestUrl = this.urlMap.get(type).get(dateFilter);
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

    // TODO(anyone): Use URLSearchParams
    private getEventUrlMap(): Map<DateFilter, string> {
        const eventUrlMap = new Map<DateFilter, string>();
        eventUrlMap.set(DateFilter.year2015, "api/events.json?from=2015-01-01&to=2015-12-31");

        const today = new Date();
        eventUrlMap.set(DateFilter.year2016, `api/events.json?from=2016-01-01&to=${Helper.dateToYMD(today)}`);

        const aMonthBefore = Helper.subtract30Days(today);
        eventUrlMap.set(DateFilter.upcoming, `api/events.json?from=${Helper.dateToYMD(aMonthBefore)}`);

        eventUrlMap.set(DateFilter.all, "api/events.json");

        return eventUrlMap;
    }

    // TODO(anyone): Use URLSearchParams
    private getFBPagesUrlMap(): Map<DateFilter, string> {
        const fpPagesUrlMap = new Map<DateFilter, string>();
        fpPagesUrlMap.set(DateFilter.all, "api/facebook.json");

        return fpPagesUrlMap;
    }

    private initializeUrlMap() {
        this.urlMap.set(MapObjectType.EVENTS, this.getEventUrlMap());
        this.urlMap.set(MapObjectType.FACEBOOK_PAGES, this.getFBPagesUrlMap());
    }
}
