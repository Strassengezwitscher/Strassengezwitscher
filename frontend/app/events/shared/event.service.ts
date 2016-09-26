import { Injectable } from "@angular/core";
import { Http, Jsonp, Response, URLSearchParams } from "@angular/http";

import { Event } from "./";
import { Observable } from "rxjs/Observable";
import "rxjs/add/observable/throw";

@Injectable()
export class EventService {
    private twitterOembedUrl = "https://api.twitter.com/1.1/statuses/oembed.json";
    private eventPageUrl = "api/events/";
    private lastEvent: Event = null;

    constructor(private http: Http, private jsonp: Jsonp) {}

    public getEvent(id: number): Observable<Event> {
        if (this.lastEvent != null && this.lastEvent.id === id) {
            return Observable.of(this.lastEvent);
        }
        return this.http.get(this.eventPageUrl + id + "/")
            .map(this.extractData)
            .do(event => this.lastEvent = event)
            .catch(this.handleError);
    }

    public getTweetIds(event: Event): Observable<string[]> {
        let tweet1Id = "778596668266647552";
        let tweet2Id = "777941364206108672";
        let tweet3Id = "777939034450620416";
        return Observable.of([tweet1Id, tweet2Id, tweet3Id]);
    }

    public getTweet(tweetId: string): Observable<string> {
        let params: URLSearchParams = new URLSearchParams();
        params.set("id", tweetId);
        params.set("callback", "JSONP_CALLBACK");
        params.set("omit_script", "true");
        return this.jsonp.request(this.twitterOembedUrl, {search: params})
            .map((response) => <string> response.json()["html"])
            .catch(error => Observable.of(""));  // suppress error
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
