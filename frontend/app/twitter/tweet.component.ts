import { Component, ViewChild, AfterViewInit, Input } from "@angular/core";
import { Observable } from "rxjs/Observable";

import {  EventService } from "../events";

declare var twttr: {widgets: {load: Function}};

@Component({
    moduleId: module.id,
    selector: "cg-tweet",
    templateUrl: "tweet.component.html",
})
export class TweetComponent implements AfterViewInit {
    @Input() private id: string;
    @ViewChild("tweetWrapper") private tweetWrapper;

    private inner: Observable<string>;
    private hidden: boolean = true;

    constructor(private eventService: EventService) {}

    public ngAfterViewInit() {
        let tweetWrapper = this.tweetWrapper;
        let observer = new MutationObserver(() => {
            twttr.widgets.load(tweetWrapper.nativeElement).then(() => this.hidden = false);
        });
        let config = { attributes: true };
        observer.observe(this.tweetWrapper.nativeElement, config);

        this.inner = this.eventService.getTweet(this.id);
    }

    public displayStyle() {
        return this.hidden ? "none" : "block";
    }
}
