import { Component, ViewChild, AfterViewInit, OnInit, Input } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";
import { Observable } from "rxjs/Observable";

import { Event, EventService } from "./../";

declare var twttr: {widgets: {load: Function}};


@Component({
    moduleId: module.id,
    selector: "cg-tweet",
    template: `
        <div [style.display]="displayStyle()" [innerHtml]="inner | async" #tweetWrapper></div>
    `,
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

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
})
export class EventDetailComponent implements OnInit {
    public tweetIds: Observable<string[]> = this.eventService.getTweetIds(this.event);
    private event: Event;
    private errorMessage: string;

    constructor(private eventService: EventService, private route: ActivatedRoute) {}

    public ngOnInit() {
        this.route.params.forEach((params: Params) => {
            let id = + params["id"];
            this.getEvent(id);
        });
    }

    public clearError() {
        this.errorMessage = "";
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.event = event,
            error => this.setErrorMessage(<any> error),
        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }
}
