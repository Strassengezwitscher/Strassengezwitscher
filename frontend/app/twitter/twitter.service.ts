import { Injectable } from "@angular/core";
import { Jsonp, URLSearchParams } from "@angular/http";

import { Observable } from "rxjs/Observable";

@Injectable()
export class TwitterService {
    private twitterOembedUrl = "https://api.twitter.com/1.1/statuses/oembed.json";

    constructor(private jsonp: Jsonp) {}

    public getTweet(tweetId: string): Observable<string> {
        let params: URLSearchParams = new URLSearchParams();
        params.set("id", tweetId);
        params.set("callback", "JSONP_CALLBACK");
        params.set("omit_script", "true");
        params.set("align", "center");
        return this.jsonp.request(this.twitterOembedUrl, {search: params})
            .map((response) => <string> response.json().html)
            .catch(error => Observable.of(""));  // suppress error
    }
}
