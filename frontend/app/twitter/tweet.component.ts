import { Component, AfterViewInit, Input, ViewChild } from "@angular/core";

declare var twttr: {widgets: any};
declare var window: any;

@Component({
    moduleId: module.id,
    selector: "cg-tweet",
    templateUrl: "tweet.component.html",
})
export class TweetComponent implements AfterViewInit {
    @Input() public id: string;
    @ViewChild("tweetWrapper") public tweetWrapper;

    public ngAfterViewInit() {
        twttr.widgets.createTweet(this.id, this.tweetWrapper.nativeElement, {
            align: "center",
        });
    }
}
