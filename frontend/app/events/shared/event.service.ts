import { Injectable } from "@angular/core";
import { Http, Response } from "@angular/http";

import { Event } from "./";
import { Observable } from "rxjs/Observable";
import "rxjs/add/observable/throw";

@Injectable()
export class EventService {
    private eventBaseUrl = "api/events/";
    private lastEvent: Event = null;

    constructor(private http: Http) {}

    public getEvent(id: number): Observable<Event> {
        if (this.lastEvent != null && this.lastEvent.id === id) {
            return Observable.of(this.lastEvent);
        }
        return this.http.get(this.eventUrl(id))
            .map(this.extractEventData)
            .do(event => this.lastEvent = event)
            .catch(this.handleError);
    }

    public getTweetIds(event: Event): Observable<string[]> {
        return this.http.get(this.tweetsUrl(event.id))
            .map(this.extractTweetData)
            .catch(error => Observable.of([]));
    }

    private eventUrl(eventId: number): string {
        return `${this.eventBaseUrl}${eventId}`;
    }

    private tweetsUrl(eventId: number): string {
        return `${this.eventUrl(eventId)}/tweets.json`;
    }

    private extractEventData(response: Response): Event {
        let data = response.json();
        return <Event> data;
    }

    private extractTweetData(response: Response): string[] {
        let data = response.json() || [];
        return <string[]> data;
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
