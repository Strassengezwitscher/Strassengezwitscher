import { Component, OnInit } from "@angular/core";

@Component({
    selector: "map-app",
    templateUrl: "map.component.html"
})
export class MapComponent implements OnInit {
    public tweets: Array<Object>;

    constructor() {
        this.tweets = [
            {
                "author": "Foo",
                "text": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt u..."
            },
            {
                "author": "Bar",
                "text": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore m..."
            },
            {
                "author": "Baz",
                "text": "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,..."
            }
        ];
    }

    ngOnInit() {
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
