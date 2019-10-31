import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PodcastsComponent } from './podcasts/podcasts.component';
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [
  { path: 'podcasts', component: PodcastsComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 
  
}