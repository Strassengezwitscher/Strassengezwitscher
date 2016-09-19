import { Component, OnInit } from "@angular/core";
import { ActivatedRoute, Params } from "@angular/router";

import { Event, EventService } from "./../";

@Component({
    moduleId: module.id,
    selector: "cg-event-detail-page",
    templateUrl: "eventDetail.component.html",
    providers: [EventService],
})

export class EventDetailComponent implements OnInit {
    private activeEvent: Event;
    private errorMessage: string;
    constructor(private eventService: EventService, private route: ActivatedRoute) {
        this.activeEvent = new Event();
    }

    public ngOnInit(): void {
        this.route.params.forEach((params: Params) => {
          let id = + params["id"];
          this.getEventDetails(id);
        });
    }

    public clearError() {
        this.errorMessage = "";
    }

    private getEventDetails(id: number) {
        this.eventService.getEvent(id)
                        .subscribe(
                            event => this.setActiveEvent(event),
                            error => this.setErrorMessage(error),
                        );
    }

    private setErrorMessage(errorMessage: string) {
        this.errorMessage = errorMessage;
    }

    private setActiveEvent(event: Event) {
        this.activeEvent = event;
    }
}
