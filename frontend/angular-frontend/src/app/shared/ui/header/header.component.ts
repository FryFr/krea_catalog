import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CartStateService } from '../../data-access/cart-state.service';
import { ProductFormComponent } from '../../../products/features/product-form/product-form.component';
import { Product } from '../../interfaces/product.interface';
import { ProductsService } from '../../../products/data-access/products.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, ProductFormComponent],
  templateUrl: './header.component.html',
  styles: ``,
})
export class HeaderComponent {
  cartState = inject(CartStateService).state;
  showCreateForm = false;

  constructor(private productsService: ProductsService) {}

  openCreateProductForm(event: Event) {
    event.preventDefault();
    this.showCreateForm = true;
  }

  onProductCreate(product: Product) {
    this.productsService.createProduct(product).subscribe(newProduct => {
      console.log('Producto creado:', newProduct);
      this.showCreateForm = false;
    });
  }
}
