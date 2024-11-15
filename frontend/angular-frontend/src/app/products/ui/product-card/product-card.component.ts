import { Component, input, output } from '@angular/core';
import { Product } from '../../../shared/interfaces/product.interface';
import { RouterLink } from '@angular/router';
import { ProductFormComponent } from '../../features/product-form/product-form.component';
import { ProductsService } from '../../data-access/products.service';

@Component({
  selector: 'app-product-card',
  standalone: true,
  imports: [RouterLink, ProductFormComponent],
  templateUrl: './product-card.component.html',
  styles: ``,
})
export class ProductCardComponent {
  product = input.required<Product>();
  showForm = false;

  addToCart = output<Product>();
  editProduct = output<Product>();
  deleteProduct = output<Product>();

  constructor(private productsService: ProductsService) {}

  add(event: Event) {
    event.stopPropagation();
    event.preventDefault();
    this.addToCart.emit(this.product());
  }

  edit(event: Event) {
    event.stopPropagation();
    event.preventDefault();
    this.showForm = true;
  }

  delete(event: Event) {
    event.stopPropagation();
    event.preventDefault();
    this.productsService.deleteProduct(this.product().id).subscribe(() => {
      this.deleteProduct.emit(this.product());
    });
  }

  onFormSubmit(product: Product) {
    this.productsService.updateProduct(this.product().id, product).subscribe(updatedProduct => {
      this.editProduct.emit(updatedProduct);
      this.showForm = false;
    });
  }

  onCloseForm() {
    this.showForm = false;
  }
}
