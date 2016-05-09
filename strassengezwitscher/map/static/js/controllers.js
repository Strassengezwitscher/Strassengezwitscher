var sgApp = angular.module('strassengezwitscherApp', []);

sgApp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
}]);

sgApp.controller('MapCtrl', function ($scope) {
    $scope.tweets = [
        {
            'author': 'Foo',
            'text': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt u...'
        },
        {
            'author': 'Bar',
            'text': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore m...'
        },
        {
            'author': 'Baz',
            'text': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,...'
        }
    ];

    function init() {
        /* position Amsterdam */
        var latlng = new google.maps.LatLng(52.3731, 4.8922);

        var mapOptions = {
          center: latlng,
          scrollWheel: false,
          zoom: 13
        };

        var marker = new google.maps.Marker({
          position: latlng,
          url: '/',
          animation: google.maps.Animation.DROP
        });

        var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        marker.setMap(map);
    };
    init();
});
