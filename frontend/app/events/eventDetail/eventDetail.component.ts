import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";

import { Event } from "../shared/event.model";
import { EventService } from "../shared/event.service";

declare var twttr: any;

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
    styleUrls: ["eventDetail.component.css"],
})
export class EventDetailComponent implements OnInit {
    public event: Event;
    public tweetIds: string[] = [];
    public errorMessage: string;
    public twttrIsBlocked: boolean = (typeof twttr === "undefined");
    private last_tweet_id: string = "0";

    constructor(private eventService: EventService, private route: ActivatedRoute) {}

    public ngOnInit() {
        this.route.params.forEach((params: Params) => {
            let id = + params["id"];
            this.getEvent(id);
        });
    }

    public refreshTweetIds() {
        this.eventService.getTweetIds(this.event, this.last_tweet_id).subscribe(
            tweetIds => {
                this.tweetIds = tweetIds.concat(this.tweetIds)
                if (tweetIds.length > 0) {
                    this.last_tweet_id = tweetIds[0]
                }
            }
        );
    }

    private getEvent(id: number) {
        this.eventService.getEvent(id).subscribe(
            event => this.setEvent(event),
            error => this.setErrorMessage(<any> error),
        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }

    private setEvent(event: Event) {
        this.event = event;
        if (this.event && this.event.coverage) {
            this.refreshTweetIds();
            setInterval(() => {
                this.refreshTweetIds();
            }, 20000);
        }
    }
}
