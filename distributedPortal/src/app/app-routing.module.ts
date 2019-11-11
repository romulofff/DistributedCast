import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { PodcastsComponent } from './podcasts/podcasts.component';
import { PodcastDetailComponent } from "./podcast-detail/podcast-detail.component";

const routes: Routes = [
  // { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'podcasts', component: PodcastsComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'detail/:EpisodeID', component: PodcastDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
