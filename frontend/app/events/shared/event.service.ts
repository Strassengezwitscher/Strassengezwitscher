import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { Event } from "./";
import { Observable } from "rxjs/Observable";
import "rxjs/add/observable/throw";

@Injectable()
export class EventService {
    private eventPageUrl = "api/events/";
    private lastEvent: Event = null;

    constructor(private http: Http) {}

    public getEvent(id: number): Observable<Event> {
        if (this.lastEvent != null && this.lastEvent.id === id) {
            return new Observable<Event>(observer => {
                observer.next(this.lastEvent);
                observer.complete();
            });
        } else {
            return this.http.get(this.eventPageUrl + id + "/")
                            .map(this.extractData)
                            .catch(this.handleError);
        }
    }

    public setActiveEvent(event: Event) {
        this.lastEvent = event;
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
