import { Component, OnInit } from "@angular/core";

import { Tweet } from "./tweet";
import { MapService } from "./map.service";

@Component({
    selector: "map-app",
    templateUrl: "map.component.html",
    providers: [MapService]
})
export class MapComponent implements OnInit {
    tweets: Tweet[];

    constructor(private mapService: MapService) {}

    getTweets() {
        this.mapService.getTweets().then(tweets => this.tweets = tweets);
    }

    ngOnInit() {
        this.getTweets();

        const latlng = new google.maps.LatLng(52.3731, 4.8922);

        const mapOptions = {
          center: latlng,
          scrollWheel: false,
          zoom: 13
        };

        const marker = new google.maps.Marker({
          position: latlng,
          animation: google.maps.Animation.DROP
        });

        const map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        marker.setMap(map);
    }
}
