import { Component, AfterViewInit, Input } from "@angular/core";
import { Observable } from "rxjs/Observable";

import { TwitterService } from "./twitter.service";

declare var twttr: {widgets: {load: Function}};
declare var window: any;

@Component({
    moduleId: module.id,
    selector: "cg-tweet",
    templateUrl: "tweet.component.html",
})
export class TweetComponent implements AfterViewInit {
    @Input() public id: string;

    public inner: Observable<string>;
    public hidden: boolean = true;

    constructor(private twitterService: TwitterService) {}

    public ngAfterViewInit() {
        this.inner = this.twitterService.getTweet(this.id);
    }

    public update(event) {
        twttr.widgets.load(event.target).then(() => this.hidden = false);
    }

    public displayStyle() {
        return this.hidden ? "none" : "block";
    }
}
