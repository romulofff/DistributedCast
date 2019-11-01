import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Podcast } from '../podcast';
import { PodcastService } from '../podcast.service';

@Component({
  selector: 'app-podcast-detail',
  templateUrl: './podcast-detail.component.html',
  styleUrls: ['./podcast-detail.component.css']
})
export class PodcastDetailComponent implements OnInit {

  podcast: Podcast;
  
  constructor(
    private route: ActivatedRoute,
    private podcastService: PodcastService,
    private location: Location
  ) { }

  ngOnInit(): void {
    this.getPodcast();
  }

  getPodcast(): void {
    const EpisodeID = +this.route.snapshot.paramMap.get('EpisodeID');
    this.podcastService.getPodcast(EpisodeID)
      .subscribe(podcast => this.podcast = podcast);
  }

  goBack(): void {
    this.location.back();
  }
}
