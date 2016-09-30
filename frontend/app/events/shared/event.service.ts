import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { Event } from "./event.model";
import { Observable } from "rxjs/Observable";
import "rxjs/add/observable/throw";

@Injectable()
export class EventService {
    private eventPageUrl = "api/events/";
    private lastEvent: Event = null;

    constructor(private http: Http) {}

    public getEvent(id: number): Observable<Event> {
        return (this.lastEvent != null && this.lastEvent.id === id) ?
                Observable.of(this.lastEvent) :
                this.http.get(this.eventPageUrl + id + "/")
                            .map(this.extractData)
                            .do(event => this.lastEvent = event)
                            .catch(this.handleError);
    }

    private extractData(response: Response): Event {
        let data = response.json();
        return <Event> data;
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
